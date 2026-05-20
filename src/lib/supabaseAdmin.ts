import { createClient } from '@supabase/supabase-js';
import { VITE_SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY } from '$env/static/private';

export const supabaseAdmin = createClient(VITE_SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY);
