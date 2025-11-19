/* 
  Backdoor script to get auth info for development environment.
  It tries to verify existing token in .env.development.
  If invalid or missing, it performs a login with predefined dev user
  and updates the .env.development file with new token and user info.
*/
import fs from "fs";
import path from "path";
import axios from "axios";

const ENV_FILE = path.resolve("./.env.development");
const BACKEND_URL = "http://localhost:8000";

// Verify if token is valid
async function verifyToken(token: string): Promise<boolean> {
  try {
    const res = await axios.get(`${BACKEND_URL}/auth/verify-token/${token}`);
    return !!res.data?.valid;
  } catch {
    return false;
  }
}

// Manual login to get a new token
async function login() {
  const username = "user@dev.com"; // predefined dev user
  const password = "passdev123";

  try {
    const res = await axios.post(
      `${BACKEND_URL}/auth/login`,
      new URLSearchParams({ username, password }),
      { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
    );

    return res.data;
  } catch (error: any) {
    if (error.response?.status === 400 || error.response?.status === 401) {
      throw new Error("DEV_USER_NOT_REGISTERED");
    }
    throw error;
  }
}

// Helper to set or update env variable
function setEnvValue(content: string, key: string, value: string) {
  const regex = new RegExp(`^${key}=.*$`, "m");
  if (regex.test(content)) {
    return content.replace(regex, `${key}=${value}`);
  } else {
    return content + `\n${key}=${value}`;
  }
}

(async () => {
  let envContent = "";

  // Read or create .env.development
  try {
    envContent = fs.readFileSync(ENV_FILE, "utf8");
  } catch {
    console.log("Creating new .env.development...");
    envContent = "";
  }

  // Extract existing token
  const existingTokenMatch = envContent.match(/^WXT_DEV_TOKEN=(.*)$/m);
  const existingToken = existingTokenMatch ? existingTokenMatch[1] : null;

  const isValid = existingToken ? await verifyToken(existingToken) : false;

  if (isValid) {
    console.log("Existing token is valid. No login needed.");
    return;
  }

  console.log("Token invalid. Logging in...");

  try {
    const { access_token, user } = await login();

    // Update only the two DEV variables
    let updatedContent = envContent;
    updatedContent = setEnvValue(updatedContent, "WXT_DEV_TOKEN", access_token);
    updatedContent = setEnvValue(updatedContent, "WXT_DEV_USER", `'${JSON.stringify(user)}'`);

    fs.writeFileSync(ENV_FILE, updatedContent);

    console.log("Updated .env.development");
  } catch (error: any) {
    if (error.message === "DEV_USER_NOT_REGISTERED") {
      console.log("Dev user not registered");
      
      // Set dev token to null
      let updatedContent = envContent;
      updatedContent = setEnvValue(updatedContent, "WXT_DEV_TOKEN", "");
      
      fs.writeFileSync(ENV_FILE, updatedContent);
    } else {
      throw error;
    }
  }
})();
