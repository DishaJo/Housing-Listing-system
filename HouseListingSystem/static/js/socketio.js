document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' +location.port);
    let newRoom = room;
    joinRoom(newRoom);

    socket.on('connect', () => {
        console.log(newRoom);
    });
     //display messages
    socket.on('message', data => {
        const p = document.createElement('p');
        const span = document.createElement('span')
        const br = document.createElement('br');
        span.innerHTML = data.username +' ' +data.time_stamp;
        p.innerHTML = span.outerHTML + br.outerHTML + data.message;
        document.querySelector('#chat-section').append(p);
    });

    // send message
    document.querySelector('#send_message').onclick = () => {
        socket.send({'message':document.querySelector('#message_input').value,
                'username':username, 'room':room});
        document.querySelector('#message_input').value = '';
    }

    // room selection
//    document.querySelectorAll('.select-room').forEach(p => {
//        p.onclick = () => {
//            let newRoom = p.innerHTML;
//            if (newRoom == room) {
//                msg = `You are already in ${room} room.`
//                console.log(msg);
//            }else{
//                leaveRoom(room);
//                joinRoom(newRoom);
//                room = newRoom;
//            }
//        }
//    });
    //leave room
    function leaveRoom(room){
        socket.emit('leave', {'username':username, 'room':room});
    }

    //join room
    function joinRoom(room){
        socket.emit('join', {'username':username, 'room':room});
    }
})