document.getElementById('start-button').addEventListener('click', function() {
    // Establish WebSocket connection
    const ws = new WebSocket('ws://localhost:8765');


    ws.onopen = function() {
        console.log('WebSocket connection opened');
        ws.send('start');  // Send a start command to the server
    };

    ws.onmessage = function(event) {
        console.log('Message from server ', event.data);
        // Handle messages from the server here
    };

    ws.onclose = function() {
        console.log('WebSocket connection closed');
    };

    
});
