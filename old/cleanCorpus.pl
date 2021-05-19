#!/usr/bin/perl


use Encode;
use strict;
use warnings;
use Data::Dumper;
use Storable 'dclone';
use JSON;
use open ':encoding(UTF-8)';

use utf8;
binmode STDIN, ":utf8";
binmode STDERR, ":utf8";
binmode STDOUT, ":utf8";

sub createGraknQueries {

	my ($args) = @_;

	# Parse author file
	my %authors = ();
	open(my $fh, '<:encoding(UTF-8)', $args->{authorFile})
	  or die "Could not open file '$args->{authorFile}' $!";
    binmode $fh, ":utf8";

	while (my $author = <$fh>) {
	  chomp $author;
	  $author =~ s/^\s+|\s+$//g;
	  my @aliases = split / *\| */, $author;
	  foreach my $alias (@aliases){
		$authors{$alias} = $aliases[0]
	  }
	}


	# Parse article
	my %articles = ();
	open(my $fh2, '<:encoding(UTF-8)', $args->{corpusFile})
	  or die "Could not open file '$args->{corpusFile}' $!";
    binmode $fh2, ":utf8";

	my %metadata = ();
	my %authorCounter = ();
	my $articleNumber = 1;

	while (my $line = <$fh2>) {
	  chomp $line;
	  next if ($line =~ /^\s*$/);
	  # When we spot a new article, we store the previously
	  # parsed article info, if any.
	  if ($line =~ /^\s*\t*In / and %metadata){

		my @authorsCounts = map { "$authorCounter{$_} => $_" } keys %authorCounter;
		$metadata{"authors"} = join ";", @authorsCounts;

		# Unique adticleId
		my $uniqueID = $metadata{"subject"} ? $metadata{"subject"} : "none";
		if ($metadata{"id"}) {
			$uniqueID = $uniqueID." -- ".$metadata{"id"}
		}
		else {
			$uniqueID = $uniqueID." -- ".$articleNumber;
			$articleNumber += 1;
		}

		my $copyREF = dclone \%metadata;
		$articles{$uniqueID} = $copyREF;

		 # Reinitialise data for next article
         %metadata = ();
	     %authorCounter = ();
	  }

	  # Parsing metadata
	  if ($line =~ /^id\s*\t*:\s*\t* (?<id>.*)$/)
		  { $metadata{"id"} = $+{id} }
	  elsif ($line =~ /^series\s*\t*:\s*\t* (?<series>.*)$/)
		  { $metadata{"series"} = $+{series} }
	  elsif ($line =~ /^title\s*\t*:\s*\t* (?<title>.*)$/)
		  { $metadata{"title"} = $+{title} }
	  elsif ($line =~ /^creator\s*\t*:\s*\t* (?<creator>.*)$/)
		  { $metadata{"creator"} = $+{creator} }
	  elsif ($line =~ /^source\s*\t*:\s*\t* (?<source>.*)$/)
		  { $metadata{"source"} = $+{source} }
	  elsif ($line =~ /^created\s*\t*:\s*\t* (?<created>.*)$/)
		  { $metadata{"created"} = $+{created} }
	  elsif ($line =~ /^pages\s*\t*:\s*\t* (?<pages>.*)$/)
		  { $metadata{"pages"} = $+{pages} }
	  elsif ($line =~ /^subject\s*\t*:[^–]*\s*(?<subject>.*)$/)
		  { $metadata{"subject"} = $+{subject} }
	  else{
		  # Parsing cited authors
		  # $line = lc $line;
		  for my $a (keys %authors){
			$authorCounter{$authors{$a}} += 1 if ($line =~ /$a/)
		  }
	  }
    }

	my $json = JSON->new->encode(\%articles);
	#my $json = JSON->new->utf8->encode(\%articles);

	print STDOUT $json;
}

createGraknQueries({
	authorFile  => $ARGV[0],
	corpusFile  => $ARGV[1],
});

