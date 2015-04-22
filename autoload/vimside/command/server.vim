function! vimside#command#server#StartEnsime()
python << EOF
import vimside.command
import vimside.env

vimside.command.StartEnsime(vimside.env.getEnv())
EOF
endfunction

function! vimside#command#server#StopEnsime()
python << EOF
import vimside.command
import vimside.env

vimside.command.StopEnsime(vimside.env.getEnv())
EOF

endfunction
