import { useState, useEffect } from "react";
import { createClient } from "@supabase/supabase-js";
import { Auth } from "@supabase/auth-ui-react";

const supabase = createClient(
  "https://srqijewflsvgaffwybfj.supabase.co/",
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNycWlqZXdmbHN2Z2FmZnd5YmZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU5MDY1MjAsImV4cCI6MjA0MTQ4MjUyMH0.GOzkNzj9XB2J3Uk-4n7bh4btZrWDLfbVelIFpuUhpB0"
);

function Login() {
  const [session, setSession] = useState(null);
  const [loggedInUser, setLoggedInUser] = useState(null);

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
  } else {
    return <div className='text-white'>Logged in: {loggedInUser}!</div>;
  }
}

export default Login;
