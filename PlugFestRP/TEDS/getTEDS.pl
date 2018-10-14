#!/usr/bin/perl
use warnings;
use strict;

my $ip;
open(my $ipcmd, "ip -4 addr show dev wlan0|") or die "Error in ip cmd";
while(<$ipcmd>){
	my $line = $_;
	if($line =~ /inet/){
		$line =~ s/.*\.(\d+)\/.*$/$1/;
		$ip = $line+0;
	}
}
my $tedsfilename = "ALPS-$ip-TEDS.txt";
system ("/bin/rm -f TEDS-*.txt $tedsfilename");
system("/usr/bin/wget --no-cache https://raw.githubusercontent.com/wiki/westewest/PlugFest/TEDS/$tedsfilename -O $tedsfilename");
open(my $tedsfile, $tedsfilename) or die "Error No TEDS file ($tedsfilename)";
my $chapter;
my $type;
while(<$tedsfile>){
	my $line = $_;
	$line =~ s/[\r\n]+//g;
	if(/^\+/){
		$chapter = $line;
		$chapter =~ s/^\+//;
		$chapter =~ s/^\s//g;
		print "Processing: $chapter\n";
		next;
	}
	if(/^=/){
		$type = $line;
		$type =~ s/^\=//;
		$type =~ s/^\s//g;
		next;
	}
	if(!($line =~ /^\s+$/)){
		open(my $fo, ">>TEDS-$type-$chapter.txt");
		print $fo $line."\n";
		close($fo);
	}

}
