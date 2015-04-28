python << EOF
import vimside.env
import vimside.vim.typeinfo

env = vimside.env.getEnv()
EOF
function! vimside#command#typeinfo#StatusTypeInfo()
  let file = expand("%:p")
  let c = col(".")
  call pyeval('vimside.vim.typeinfo.showTypeAt(env, "'.file.'", '. c . ')')
endfunction
