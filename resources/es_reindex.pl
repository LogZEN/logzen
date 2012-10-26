use ElasticSearch;
use Data::Dumper;

my $es = ElasticSearch->new(
	servers      => '127.0.0.1:9200',
	transport    => 'http'
);

my $source = $es->scrolled_search(
	index       => 'syslog',
	search_type => 'scan',
	scroll      => '5m',
	version     => 1
);

$es->reindex(
	source      => $source,
	dest_index  => 'syslog_new',
	transform   => sub {
		my $doc = shift;
		
		my $x = $doc->{_source};
		
		my $time = $x->{date};
		my $host = $x->{host};
		
		my $severity = $x->{severity};
		     if($severity eq 'emerg'  ) { $severity = 0;
		} elsif($severity eq 'panic'  ) { $severity = 0;
		} elsif($severity eq 'alert'  ) { $severity = 1;
		} elsif($severity eq 'crit'   ) { $severity = 2;
		} elsif($severity eq 'err'    ) { $severity = 3;
		} elsif($severity eq 'error'  ) { $severity = 3;
		} elsif($severity eq 'warning') { $severity = 4;
		} elsif($severity eq 'warn'   ) { $severity = 4;
		} elsif($severity eq 'notice' ) { $severity = 5;
		} elsif($severity eq 'info'   ) { $severity = 6;
		} elsif($severity eq 'debug'  ) { $severity = 7;
		}
		
		my $facility = $x->{facility};
		     if($facility eq 'kern'    ) { $facility = 0;
		} elsif($facility eq 'user'    ) { $facility = 1;
		} elsif($facility eq 'mail'    ) { $facility = 2;
		} elsif($facility eq 'daemon'  ) { $facility = 3;
		} elsif($facility eq 'auth'    ) { $facility = 4;
		} elsif($facility eq 'syslog'  ) { $facility = 5;
		} elsif($facility eq 'lpr'     ) { $facility = 6;
		} elsif($facility eq 'news'    ) { $facility = 7;
		} elsif($facility eq 'uucp'    ) { $facility = 8;
		} elsif($facility eq 'cron'    ) { $facility = 9;
		} elsif($facility eq 'authpriv') { $facility = 10;
		} elsif($facility eq 'ftp'     ) { $facility = 11;
		} elsif($facility eq 'ntp'     ) { $facility = 12;
		} elsif($facility eq 'auth'    ) { $facility = 13;
		} elsif($facility eq 'auth'    ) { $facility = 14;
		} elsif($facility eq 'cron'    ) { $facility = 15;
		} elsif($facility eq 'local0'  ) { $facility = 16;
		} elsif($facility eq 'local1'  ) { $facility = 17;
		} elsif($facility eq 'local2'  ) { $facility = 18;
		} elsif($facility eq 'local3'  ) { $facility = 19;
		} elsif($facility eq 'local4'  ) { $facility = 20;
		} elsif($facility eq 'local5'  ) { $facility = 21;
		} elsif($facility eq 'local6'  ) { $facility = 22;
		} elsif($facility eq 'local7'  ) { $facility = 23;
		}

		my $program = $x->{program};
		my $message = $x->{message};
		
		$doc->{_source} = {
			"time" => $date,
			"host" => $host,
			"severity" => $severity,
			"facility" => $facility,
			"program" => $program,
			"message" => $message,
		};
		
		return $doc;
	}
);
