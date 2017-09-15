var manualChangeMade = false;

function change_code(changeObj) {
    window.codeMirror.replaceRange(
        changeObj.text.join('\n'),
        changeObj.from,
        changeObj.to
    );
}

function init_socket_io() {
    var socket = io.connect('/');

    socket.on('connect', function() {
        console.log('connected!');
    });

    socket.on('code', function (code) {
        manualChangeMade = true;
        window.codeMirror.setValue(code);
    });

    socket.on('code change', function (changes) {
        manualChangeMade = true;
        window.codeMirror.operation(() => changes.forEach(change_code));
    });

    return socket;
}

function init() {
    window.codeMirror = CodeMirror(document.body, {
        mode: 'python'
    });

    window.socket = init_socket_io();

    var pendingChanges = [];
    var changeTimeout = null;

    function makeChanges () {
        window.socket.emit('code change', {
            changes: pendingChanges
        });
        pendingChanges = [];
    }

    window.codeMirror.on('changes', function (e, changes) {
        if (manualChangeMade) {
            manualChangeMade = false;
            return;
        }

        pendingChanges = pendingChanges.concat(changes);
        
        clearTimeout(changeTimeout);
        changeTimeout = setTimeout(makeChanges, 100);
    });
}

window.addEventListener('load', init);
