#!/usr/bin/env ruby

f = File.open("dane.dat", "rt")

xh, yh = f.gets.split("\t")
print "Header: #{xh}, #{yh}"

#TODO read last_choice
#store values as array of hashes
#[{'phi' => '0.2', 'Z' => '1000', 'diam' = 20, ...}, {'phi' => '0.18', 'Z' => '900', 'diam' = 20, ...}]
#write this stuff into one file, fixed order of columns --> AutoIt
