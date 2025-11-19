import { apiFetch, API_BASE } from "./api";


// Backend API call to register a new user
export async function registerUser( data :{
    name: string;
    email: string;
    password: string;
} ): Promise<any> {

    const res = await fetch(`${API_BASE}/auth/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })

    if (!res.ok) {
        throw new Error("Failed to register user");
    }

    return res.json();
}



// Backend API call to login a user
export async function loginUser( data :{
    username: string;
    password: string;
} ): Promise<any> {
    const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams(data).toString(),
    })

    if (!res.ok) {
        throw new Error("Failed to login user");
    }

    return res.json();
}
