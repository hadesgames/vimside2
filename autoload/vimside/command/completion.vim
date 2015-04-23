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
