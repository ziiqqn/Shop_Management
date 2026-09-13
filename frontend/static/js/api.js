/**
 * 统一封装 axios：
 * - 自动加 Authorization 头
 * - 401 自动跳登录页
 * - 统一错误提示
 */

const BASE_URL = "https://shopmanagement-production-bd53.up.railway.app/";

const api = axios.create({
    baseURL: BASE_URL,
    timeout: 10000
});

// 请求拦截器：自动加 token
api.interceptors.request.use(
    config => {
        const token = localStorage.getItem("token");
        if (token) {
            config.headers["Authorization"] = `Bearer ${token}`;
        }
        return config;
    },
    error => Promise.reject(error)
);

// 响应拦截器：统一错误处理
api.interceptors.response.use(
    res => res.data,
    error => {
        const status = error.response?.status;
        const detail = error.response?.data?.detail || error.message;

        if (status === 401) {
            // token 无效，清除并跳登录
            localStorage.clear();
            if (!location.pathname.endsWith("index.html") && location.pathname !== "/") {
                alert("登录已过期，请重新登录");
                location.href = getRootPath() + "index.html";
            }
        } else {
            showToast(detail, "error");
        }
        return Promise.reject(error);
    }
);

/* ============ 工具函数 ============ */

// 计算根路径（用于多级目录跳转）
function getRootPath() {
    const path = location.pathname;
    if (path.includes("/pages/")) {
        return path.substring(0, path.indexOf("/pages/") + 1);
    }
    return "./";
}

// 轻提示
function showToast(message, type = "info") {
    const el = document.createElement("div");
    el.className = `toast toast-${type}`;
    el.textContent = message;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 2500);
}

// 退出登录
function logout() {
    localStorage.clear();
    location.href = getRootPath() + "index.html";
}

// 从 token 中解析角色（简单解析，不做签名校验）
function getRole() {
    return localStorage.getItem("role") || "";
}

function getUsername() {
    return localStorage.getItem("username") || "";
}