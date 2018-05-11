#!/usr/bin/env perl

use strict;
use warnings;
use Getopt::Long;

my $front;
my $back;
my $both;
my $DEBUG=1;

GetOptions(
    'back' =>\$back,
    'front' =>\$front,
    'both' =>\$both,
);

if(!defined $front && !defined $back) {
    $both=1;
}


while (<>) {
    if($both){
        s/\s*$/\n/ ;
        s/^\s*// ;
    }
    else {
        s/\s*$/\n/ if $back;
        s/^\s*// if $front;
    }


    print;
}


