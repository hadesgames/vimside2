python << EOF
import vimside.env
import vimside.command
env = vimside.env.getEnv()

EOF


let s:completions = {}
function! vimside#command#completion#Complete(findstart, base)
  let file = expand('%:p')
  let offset = line2byte(line("."))+col(".") - 2
  if a:findstart
    w
    let result = pyeval('env.completions.get_completions("'.file.'", '. offset . ')')
    let s:completions = result["completions"]
    return col('.') - len(result["prefix"]) - 1
  else
    let result = s:completions
    let s:completions = {}

    return result
  endif

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
