import { Outlet } from "react-router-dom";
import { useState, useEffect } from "react";
import useRefreshToken from "../../../api/useRefreshToken";
import { useAuth } from "../AuthContext";


const PersistLogin = () => {
  const { accessToken } = useAuth();
  const refresh = useRefreshToken();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const verifyRefresh = async () => {
        try {
            await refresh();
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