const { createApp, ref, reactive, onMounted, watch } = Vue;

createApp({
    setup() {
        const username = ref(getUsername());
        const view = ref("shops");
        const shops = ref([]);
        const loading = ref(false);

        const empForm = reactive({
            jobNumber: "",
            name: "",
            password: "",
            department: "",
            rank: "员工"
        });

        const loadShops = async () => {
            try {
                shops.value = await api.get("/api/shop/list");
            } catch (e) {}
        };

        const submitEmployee = async () => {
            if (!empForm.jobNumber || !empForm.name || !empForm.password || !empForm.department) {
                showToast("请填写完整信息", "error");
                return;
            }
            loading.value = true;
            try {
                await api.post("/api/employee/register", empForm);
                showToast("员工注册成功", "success");
                Object.assign(empForm, {
                    jobNumber: "", name: "", password: "",
                    department: "", rank: "员工"
                });
            } catch (e) {}
            finally {
                loading.value = false;
            }
        };

        onMounted(loadShops);

        watch(view, v => {
            if (v === "shops") loadShops();
        });

        return {
            username, view, shops, loadShops,
            empForm, loading, submitEmployee, logout
        };
    }
}).mount("#app");