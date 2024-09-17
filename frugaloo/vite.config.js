import react from '@vitejs/plugin-react'
import { defineConfig, loadEnv } from 'vite'


// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  return {
    define: {
      'process.env.VITE_SUPABASE_CLIENT': JSON.stringify(env.VITE_SUPABASE_CLIENT),
      'process.env.VITE_SUPABASE_SECRET': JSON.stringify(env.VITE_SUPABASE_SECRET)

    },
    plugins: [react()],
  }
})
