const { createApp, ref, reactive, computed, onMounted } = Vue;

createApp({
    setup() {
        const role = ref(getRole());
        const username = ref(getUsername());

        // 菜单配置（按角色）
        const allMenus = {
            INVESTMENT: [
                { key: "tenant", label: "租户管理" },
                { key: "contract", label: "合同管理" },
                { key: "rent", label: "租金管理" }
            ],
            FINANCE: [
                { key: "audit", label: "合同审核" }
            ],
            OPERATION: [
                { key: "rentUpdate", label: "租金修改" },
                { key: "shopExit", label: "商铺退租" }
            ],
            CASHIER: [
                { key: "receipt", label: "收款单管理" }
            ]
        };

        const roleNameMap = {
            INVESTMENT: "招商",
            FINANCE: "财务",
            OPERATION: "营运",
            CASHIER: "收银"
        };

        const menus = computed(() => allMenus[role.value] || []);
        const roleName = computed(() => roleNameMap[role.value] || "员工");
        const view = ref(menus.value[0]?.key || "");

        const currentTitle = computed(() => {
            const m = menus.value.find(x => x.key === view.value);
            return m ? m.label : roleName.value + "工作台";
        });

        /* ============= 数据状态 ============= */
        const tenants = ref([]);
        const contracts = ref([]);
        const rents = ref([]);
        const receipts = ref([]);
        const rentedShops = ref([]);

        /* ============= 弹窗状态 ============= */
        const showTenantModal = ref(false);
        const tenantForm = reactive({ name: "", idCard: "", brandType: "个体", brandName: "" });

        const showRentModal = ref(false);
        const rentForm = reactive({ id: null, rentType: "", unitPrice: null, percentRate: null });

        const showPaidModal = ref(false);
        const paidForm = reactive({ id: null, amount: 0 });

        /* ============= 数据加载 ============= */
        const loadTenants = async () => {
            try { tenants.value = await api.get("/api/tenant/list"); } catch (e) {}
        };

        const loadContracts = async () => {
            try { contracts.value = await api.get("/api/contract/list"); } catch (e) {}
        };

        const loadRents = async () => {
            try { rents.value = await api.get("/api/rent/list"); } catch (e) {}
        };

        const loadReceipts = async () => {
            try { receipts.value = await api.get("/api/receipt/list"); } catch (e) {}
        };

        const loadRentedShops = async () => {
            try {
                const shops = await api.get("/api/shop/list");
                rentedShops.value = shops.filter(s => s.isRented === 1);
            } catch (e) {}
        };

        /* ============= 业务操作 ============= */
        const submitTenant = async () => {
            if (!tenantForm.name || !tenantForm.idCard) {
                showToast("请填写完整信息", "error");
                return;
            }
            await api.post("/api/tenant/add", tenantForm);
            showToast("新增成功", "success");
            showTenantModal.value = false;
            Object.assign(tenantForm, { name: "", idCard: "", brandType: "个体", brandName: "" });
            loadTenants();
        };

        const audit = async (contractId, approved) => {
            if (!confirm(`确定${approved ? "通过" : "不通过"}该合同吗？`)) return;
            await api.put(`/api/contract/audit/${contractId}`, { approved, remark: "" });
            showToast("审核完成", "success");
            loadContracts();
        };

        const editRent = (r) => {
            Object.assign(rentForm, r);
            showRentModal.value = true;
        };

        const submitRent = async () => {
            await api.put("/api/rent/update", rentForm);
            showToast("修改成功", "success");
            showRentModal.value = false;
            loadRents();
        };

        const remind = async (id) => {
            await api.put(`/api/receipt/remind/${id}`);
            showToast("催收已发送", "success");
            loadReceipts();
        };

        const editPaid = (r) => {
            paidForm.id = r.id;
            paidForm.amount = r.paidAmount;
            showPaidModal.value = true;
        };

        const submitPaid = async () => {
            await api.put(`/api/receipt/paid/${paidForm.id}?amount=${paidForm.amount}`);
            showToast("修改成功", "success");
            showPaidModal.value = false;
            loadReceipts();
        };

        const exitShop = async (shop) => {
            if (!confirm(`确定对商铺 ${shop.shopNumber} 退租吗？`)) return;
            await api.put(`/api/shop/exit/${shop.id}`);
            showToast("退租成功", "success");
            loadRentedShops();
        };

        /* ============= 工具 ============= */
        const auditText = (s) => ({ 0: "待审核", 1: "已通过", 2: "未通过" }[s] || "未知");
        const auditTag = (s) => ({ 0: "tag-warning", 1: "tag-success", 2: "tag-danger" }[s] || "tag-info");

        /* ============= 初始化 ============= */
        onMounted(() => {
            if (view.value === "tenant") loadTenants();
            else if (view.value === "contract" || view.value === "audit") loadContracts();
            else if (view.value === "rent" || view.value === "rentUpdate") loadRents();
            else if (view.value === "receipt") loadReceipts();
            else if (view.value === "shopExit") loadRentedShops();
        });

        // 监听菜单切换时自动加载数据
        const { watch } = Vue;
        watch(view, (v) => {
            if (v === "tenant") loadTenants();
            else if (v === "contract" || v === "audit") loadContracts();
            else if (v === "rent" || v === "rentUpdate") loadRents();
            else if (v === "receipt") loadReceipts();
            else if (v === "shopExit") loadRentedShops();
        });

        return {
            role, username, roleName, menus, view, currentTitle,
            tenants, contracts, rents, receipts, rentedShops,
            showTenantModal, tenantForm, submitTenant,
            showRentModal, rentForm, editRent, submitRent,
            showPaidModal, paidForm, editPaid, submitPaid,
            loadTenants, loadContracts, loadRents, loadReceipts, loadRentedShops,
            audit, remind, exitShop,
            auditText, auditTag, logout
        };
    }
}).mount("#app");