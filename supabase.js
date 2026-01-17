import { createClient } from '@supabase/supabase-js'

const SUPABASE_URL = 'https://ackbwoickqaqvmjqtblu.supabase.co';
const SUPABASE_KEY = 'sb_publishable_LxA2FCaYHje_Q1RqboENng_5hPXkN5S';
const supabase = createClient(supabaseUrl, supabaseKey)

// Halimbawa ng pag-fetch (Palitan ang loadData function mo):
const loadData = async () => {
  const { data: booksData } = await supabase.from('books').select('*')
  books.value = booksData
  
  const { count } = await supabase.from('users').select('*', { count: 'exact', head: true })
  userCount.value = count
}