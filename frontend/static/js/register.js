const { createApp, reactive, ref } = Vue;

createApp({
    setup() {
        const loading = ref(false);
        const form = reactive({
            username: "",
            password: "",
            confirmPassword: "",
            tenantName: "",
            idCard: "",
            brandType: "",
            brandName: ""
        });

        const validate = () => {
            if (!form.username || form.username.length < 3) return "用户名至少3个字符";
            if (!form.password || form.password.length < 6) return "密码至少6位";
            if (form.password !== form.confirmPassword) return "两次密码不一致";
            if (!form.tenantName) return "请填写租户名称";
            if (!/^\d{17}[\dXx]$/.test(form.idCard)) return "身份证号格式不正确";
            if (!form.brandType) return "请选择品牌类型";
            return null;
        };

        const handleRegister = async () => {
            const err = validate();
            if (err) {
                showToast(err, "error");
                return;
            }
            loading.value = true;
            try {
                await api.post("/api/auth/merchant/register", {
                    username: form.username,
                    password: form.password,
                    tenantName: form.tenantName,
                    idCard: form.idCard,
                    brandType: form.brandType,
                    brandName: form.brandName
                });
                showToast("注册成功，请登录", "success");
                setTimeout(() => location.href = "../index.html", 1200);
            } catch (e) {
                // 错误已由拦截器处理
            } finally {
                loading.value = false;
            }
        };

        return { form, loading, handleRegister };
    }
}).mount("#app");