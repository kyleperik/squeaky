var manualChangeMade = false;
var lastChangeId = null;
var incoming_changes = [];

function change_code(changeObj) {
    window.codeMirror.replaceRange(
        changeObj.text,
        changeObj.from,
        changeObj.to
    );
}

function queue_incoming_changes(changes) {
    var all_incoming_changes = incoming_changes.concat(changes).sort((c1, c2) => c1 - c2);
    var changes_tomake = all_incoming_changes.filter((change, i) => {
        // Get only the changes coming right after the last change, without breaks
        return change.id === lastChangeId + i + 1;
    });
    incoming_changes = all_incoming_changes.filter(c => !changes_tomake.includes(c));
    console.log('incoming', all_incoming_changes);
    if (changes_tomake.length > 0) {
        lastChangeId = changes_tomake.slice(-1)[0].id;
        console.log('last changeid', lastChangeId);
        manualChangeMade = true;
        window.codeMirror.operation(() => changes_tomake.forEach(change_code));
    }
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

    socket.on('last changeid', function (changeid) {
        console.log('last changeid', changeid);
        lastChangeId = changeid;
    });

    socket.on('code change', function (changes) {
        queue_incoming_changes(changes);
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

        changes_tosend = changes.map(c => ({
            to: c.to,
            from: c.from,
            text: c.text,
            last_changeid: lastChangeId
        }));

        pendingChanges = pendingChanges.concat(changes_tosend);
        
        clearTimeout(changeTimeout);
        changeTimeout = setTimeout(makeChanges, 100);
    });
}

window.addEventListener('load', init);
