import { useEffect } from "react";
import useAxios from "../api/useAxios";

export default function Dashboard() {
  const axiosApi = useAxios();

  useEffect(() => {
  axiosApi.get("/results/11")
    .then(res => console.log(res.data))
    .catch(err => console.log("Error:", err.response?.status));
  }, [axiosApi]);

  return (
    <div>
      <h2>THE DASHBOARD</h2>
    </div>
  );
}