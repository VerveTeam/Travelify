import { useState, useEffect } from "react";
import { createClient } from "@supabase/supabase-js";
import { Auth } from "@supabase/auth-ui-react";
import { useNavigate } from "react-router-dom";

const supabase = createClient(
  process.env.VITE_SUPABASE_CLIENT,
  process.env.VITE_SUPABASE_SECRET
);

function Login() {
  const [session, setSession] = useState(null);
  const [loggedInUser, setLoggedInUser] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    supabase.auth.getSession().then(async ({ data: { session } }) => {
      setSession(session);
      if (session) {
        const {
          data: { user },
        } = await supabase.auth.getUser();
        setLoggedInUser(user.email);
      }
    });

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      if (session) {
        supabase.auth
          .getUser()
          .then(({ data: { user } }) => setLoggedInUser(user.email));
      }
    });

    return () => subscription.unsubscribe();
  }, []);

  if (!session) {
    return (
      <>
        <div className='hero min-h-screen fixed'>
          <div className='hero-content' style={{ marginTop: "-10rem" }}>
            <div className='card bg-base-100 sm:w-26 sm:w-[25] shadow-2xl p-10'>
              <div className='text-center text-2xl'>Travelify</div>
              <Auth
                supabaseClient={supabase}
                appearance={{
                  extend: false,
                  className: {
                    input:
                      "input input-bordered input-sm w-full sm:w-[400px] md:w-[500px] lg:w-[600px]", // Responsive width classes
                    label: "label text-md",
                    button: "btn btn-ghost btn-sm btn-primary mt-10",
                    container:
                      "flex flex-col space-y-2 items-center justify-center text-md",
                    divider: "divider",
                  },
                }}
                providers={["google"]}
              />
            </div>
          </div>
        </div>
      </>
    );
  }
  return navigate("/");
}

export default Login;
