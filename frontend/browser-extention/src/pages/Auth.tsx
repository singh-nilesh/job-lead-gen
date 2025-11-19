import { useAuth } from "@/core/AuthContext"
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";


export default function Auth() {

    const { login, register } = useAuth();
    const navigate = useNavigate();
    const [state, setState] = useState("login")
    
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        password: '',
    })
    const [rePassword, setRePassword] = useState('');
    const [error, setError] = useState<string | null>(null);

    // Submit handler
    const handleSubmit = async (e:any) => {
        e.preventDefault();
        setError(null);

        if (state === "register") {
            // validation: passwords match
            if (formData.password !== rePassword) {
                setError("Passwords do not match.");
                return;
            }

            // validation: check if first name and last name are provided
            if (!formData.firstName.trim() || !formData.lastName.trim()) {
                setError("Please provide both first name and last name.");
                return;
            }

            try{
                // Prepare data according to backend schema
                const registerData = {
                    name: `${formData.firstName.trim()} ${formData.lastName.trim()}`,
                    email: formData.email,
                    password: formData.password,
                };
                
                await register(registerData);
                setState("login");
                // clear sensitive fields
                setFormData(prev => ({ ...prev, password: '' }));
                setRePassword('');
            }
            catch (err){
                setError("Registration failed. Please try again.");
            }
            return;
        }

        if (state === "login") {
            try{
                await login(formData.email, formData.password);
                navigate('/home');
            } catch (err) {
                setError("Invalid email or password");
            }
        }
    }

    const handleRePasswordChange = (e:any) => {
        setRePassword(e.target.value);
    }
    
    // Form input change handler
    const handleChange = (e:any) => {
        const { name, value } = e.target
        setFormData(prev => ({ ...prev, [name]: value }))
    }

    return (
            <form onSubmit={handleSubmit} className="sm:w-[350px] w-full text-center border border-gray-300/60 rounded-2xl px-8 bg-white">
                <h1 className="text-gray-900 text-3xl mt-10 font-medium">{state === "login" ? "Login" : "Sign up"}</h1>
                <p className="text-gray-500 text-sm mt-2">Please sign in to continue</p>

                {error && (
                    <div className="text-sm text-red-600 mt-4">
                        {error}
                    </div>
                )}

                {state !== "login" && (
                    <>
                        <div className="flex items-center mt-6 w-full bg-white border border-gray-300/80 h-12 rounded-full overflow-hidden pl-6 gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6B7280" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-user-round-icon lucide-user-round"><circle cx="12" cy="8" r="5" /><path d="M20 21a8 8 0 0 0-16 0" /></svg>
                            <input type="text" name="firstName" placeholder="First Name" className="border-none outline-none ring-0" value={formData.firstName} onChange={handleChange} required />
                        </div>

                        <div className="flex items-center mt-4 w-full bg-white border border-gray-300/80 h-12 rounded-full overflow-hidden pl-6 gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6B7280" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-user-round-icon lucide-user-round"><circle cx="12" cy="8" r="5" /><path d="M20 21a8 8 0 0 0-16 0" /></svg>
                            <input type="text" name="lastName" placeholder="Last Name" className="border-none outline-none ring-0" value={formData.lastName} onChange={handleChange} required />
                        </div>
                    </>
                )}

                <div className="flex items-center w-full mt-4 bg-white border border-gray-300/80 h-12 rounded-full overflow-hidden pl-6 gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6B7280" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-mail-icon lucide-mail"><path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7" /><rect x="2" y="4" width="20" height="16" rx="2" /></svg>
                    <input type="email" name="email" placeholder="Email id" className="border-none outline-none ring-0" value={formData.email} onChange={handleChange} required />
                </div>
                <div className="flex items-center mt-4 w-full bg-white border border-gray-300/80 h-12 rounded-full overflow-hidden pl-6 gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6B7280" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-lock-icon lucide-lock"><rect width="18" height="11" x="3" y="11" rx="2" ry="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" /></svg>
                    <input type="password" name="password" placeholder="Password" className="border-none outline-none ring-0" value={formData.password} onChange={handleChange} required />
                </div>

                {state === "register" && (
                    <div className="flex items-center mt-4 w-full bg-white border border-gray-300/80 h-12 rounded-full overflow-hidden pl-6 gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6B7280" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-lock-icon lucide-lock"><rect width="18" height="11" x="3" y="11" rx="2" ry="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" /></svg>
                        <input type="password" name="rePassword" placeholder="Re-enter Password" className="border-none outline-none ring-0" value={rePassword} onChange={handleRePasswordChange} required />
                    </div>
                )}

                {state === "login" && (
                    <div className="mt-4 text-left text-indigo-500">
                        <button className="text-sm" type="reset">Forget password?</button>
                    </div>
                )}
                <button type="submit" className="mt-2 w-full h-11 rounded-full text-white bg-indigo-500 hover:opacity-90 transition-opacity">
                    {state === "login" ? "Login" : "Sign up"}
                </button>
                <p onClick={() => { setError(null); setState(prev => prev === "login" ? "register" : "login") }} className="text-gray-500 text-sm mt-3 mb-11">{state === "login" ? "Don't have an account?" : "Already have an account?"} <a href="#" className="text-indigo-500 hover:underline">click here</a></p>
            </form>
    )
}