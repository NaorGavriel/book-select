import { useEffect, useState } from "react";
import { AlertCircle } from "lucide-react";

export default function RateLimitPopup() {
    const [visible, setVisible] = useState(false);

    useEffect(() => {
        const handler = () => {
            setVisible(true);
            setTimeout(() => setVisible(false), 4000);
        };

        window.addEventListener("rate-limit", handler);
        return () => window.removeEventListener("rate-limit", handler);
    }, []);

    if (!visible) return null;

    return (
        <div className="fixed top-4 right-4 z-50">
            <div className="flex items-center gap-3 bg-linear-to-r from-neutral-800 via-neutral-900 to-violet-950 border-1
                         border-amber-200 text-slate-100 px-5 py-3 rounded-lg shadow-xl">
                <AlertCircle className="text-amber-400 w-5 h-5" />

                <span className="font-medium">
                    Too many requests. Please try again later.
                </span>

                <button
                    className="ml-2 text-slate-400 hover:text-white transition"
                    onClick={() => setVisible(false)}
                >
                    ✕
                </button>
            </div>
        </div>
    );
}