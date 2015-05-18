python << EOF
import vimside.env
import vimside.command
from vimside.vim.commands.completion import OmniComplete

env = vimside.env.getEnv()

EOF


function! vimside#command#completion#Complete(findstart, base)
  return pyeval('OmniComplete(env,'.a:findstart.', "'.a:base.'")')
endfunction

function! vimside#command#completion#SuggestImport()
  let file = expand('%:p')
  let offset = line2byte(line("."))+col(".") - 2

  let imports = pyeval('env.completions.get_import_suggestions("'.file.'", '.offset . ')')
  let index = vimside#util#prompt#ShowPrompt("use import", imports)
  let import = imports[index]


  "echo index
  call pyeval('env.refactor.execute_add_import("'.file.'", "'. import . '")')
  edit!
endfunction
