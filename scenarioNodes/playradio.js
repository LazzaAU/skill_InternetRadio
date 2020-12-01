module.exports = function(RED) {
	function playradio(config) {
		RED.nodes.createNode(this, config);
	}

	RED.nodes.registerType('playradio', playradio);
}