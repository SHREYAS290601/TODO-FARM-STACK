import { useContext } from "react";
import { AuthContext } from "../components/context/JWTAuthContext";

export const useAuth = () => useContext(AuthContext);
