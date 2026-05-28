import { Outlet } from "react-router-dom";
import { useState, useEffect } from "react";
import useRefreshToken from "../../../api/useRefreshToken";
import { useAuth } from "../AuthContext";


const PersistLogin = () => {
  const { accessToken, setIsAdmin } = useAuth();
  const refresh = useRefreshToken();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const verifyRefresh = async () => {
        try {
            const newToken = await refresh();
            const payload = JSON.parse(atob(newToken.split(".")[1]));
            setIsAdmin(payload.is_admin === true);
        } catch (err) {
            console.log(err)
        } finally {
            setLoading(false);
        }
    };

    if (!accessToken) {
        verifyRefresh();
    } else {
        setLoading(false);
    }
  }, []);

  if (loading) return <p>Loading...</p>;

  return <Outlet />;
};

export default PersistLogin;