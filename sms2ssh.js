var control = require('control'),
		task = control.task;

task('mycluster', 'Config for my cluster', function () {
	var config = {
		'kilburn.cs.man.ac.uk': {
			user: 'mbax4hb2'
		},
		'b.domain.com': {
			user: 'blogin',
			sshOptions: ['-p 44'] // sshd daemon on non-standard port
		}
	};

	return control.controllers(config);
});


task('date', 'Get date', function (controller) {
	controller.ssh('date');
});

control.begin();