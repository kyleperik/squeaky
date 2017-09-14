
function set_code(code) {
    if (code !== window.codeMirror.getValue()) {
        window.codeMirror.setValue(code);
    }
}

function init_socket_io() {
    var socket = io.connect('/');

    socket.on('connect', function() {
        console.log('connected!')
    });

    socket.on('code', function (code) {
        set_code(code);
    });

    return socket;
}

function init() {
    window.codeMirror = CodeMirror(document.body, {
        mode: 'python'
    });

    window.socket = init_socket_io();

    window.codeMirror.on('change', function (e) {
        window.socket.emit('code change', {
            data: e.getValue()
        });
    });
    console.log(window.socket);
}

window.addEventListener('load', init);
