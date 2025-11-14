// Wrapper to automaicaly inject JTW token into API requests headers

export const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function apiFetch(
    endpoint: string,
    options: RequestInit = { }
): Promise<any> {
    const token = localStorage.getItem("token");

    const header = new Headers(options.headers || {});
    header.set("Content-Type", "application/json");
    if (token) {
        header.set("Authorization", `Bearer ${token}`);
    }

    const res = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers: header,
    });

    if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        const error = new Error(res.statusText);
    }

    return res.json();
    
}