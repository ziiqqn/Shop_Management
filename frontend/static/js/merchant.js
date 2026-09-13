const { createApp, ref, reactive, onMounted } = Vue;

createApp({
    setup() {
        const username = ref(getUsername());
        const view = ref("bill");
        const bills = ref([]);
        const showPayModal = ref(false);
        const payForm = reactive({ billId: null, receivable: 0, amount: 0, channel: "wechat" });

        const loadBills = async () => {
            try {
                bills.value = await api.get("/api/bill/list");
            } catch (e) {}
        };

        const openPay = (b) => {
            payForm.billId = b.id;
            payForm.receivable = b.receivableAmount;
            payForm.amount = b.unpaidAmount;
            payForm.channel = "wechat";
            showPayModal.value = true;
        };

        const submitPay = async () => {
            if (!payForm.amount || payForm.amount <= 0) {
                showToast("请输入有效的缴费金额", "error");
                return;
            }
            try {
                await api.post(
                    `/api/bill/pay/${payForm.billId}?amount=${payForm.amount}&channel=${payForm.channel}`
                );
                showToast("缴费成功", "success");
                showPayModal.value = false;
                loadBills();
            } catch (e) {}
        };

        onMounted(loadBills);

        return {
            username, view, bills, loadBills,
            showPayModal, payForm, openPay, submitPay, logout
        };
    }
}).mount("#app");