const { createApp, reactive, ref, computed } = Vue;

createApp({
    setup() {
        const tab = ref("employee");
        const loading = ref(false);
        const form = reactive({ username: "", password: "" });

        const usernameLabel = computed(() => {
            return tab.value === "employee" ? "工号" : "用户名";
        });

        const usernamePlaceholder = computed(() => {
            if (tab.value === "employee") return "请输入工号";
            if (tab.value === "merchant") return "请输入商户用户名";
            return "请输入老板用户名";
        });

        const switchTab = (name) => {
            tab.value = name;
            form.username = "";
            form.password = "";
        };

        const handleLogin = async () => {
            if (!form.username || !form.password) {
                showToast("请填写用户名和密码", "error");
                return;
            }
            loading.value = true;
            try {
                const url = `/api/auth/${tab.value}/login`;
                const res = await api.post(url, {
                    username: form.username,
                    password: form.password
                });

                localStorage.setItem("token", res.token);
                localStorage.setItem("role", res.role);
                localStorage.setItem("username", res.username);

                showToast("登录成功", "success");

                // 根据身份跳转不同工作台
                setTimeout(() => {
                    if (tab.value === "employee") {
                        location.href = "pages/employee.html";
                    } else if (tab.value === "merchant") {
                        location.href = "pages/merchant.html";
                    } else {
                        location.href = "pages/boss.html";
                    }
                }, 600);

            } catch (err) {
                // 错误已由拦截器弹出
            } finally {
                loading.value = false;
            }
        };

        return {
            tab, loading, form,
            usernameLabel, usernamePlaceholder,
            switchTab, handleLogin
        };
    }
}).mount("#app");