define(['backbone'],
function(Backbone) {
	Host = Backbone.Model.extend({
		urlRoot:'/host/',
		defaults: {
			hostname: '',
			description: '',
			homes: '',
			tags: ''
		},
		url: function() {
			return this.urlRoot+this.get('hostname')
		}
	});
});

