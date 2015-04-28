python << EOF
import vimside.command
import vimside.env

env = vimside.env.getEnv()
EOF

function! vimside#command#server#StartEnsime()
python << EOF
vimside.command.StartEnsime(env)
EOF
endfunction

function! vimside#command#server#StopEnsime()
python << EOF
vimside.command.StopEnsime(env)
EOF
endfunction

function! vimside#command#server#ReloadCurrentFile()
  let file = expand("%:p")
  call pyeval('vimside.command.ReloadFile(env,"'. file .'")')
endfunction
