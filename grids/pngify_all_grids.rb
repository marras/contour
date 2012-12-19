#!/usr/bin/env ruby

require 'pry'

def do_whats_necessary(file, d)
  `cp #{file} ..`
  arr = d.split('/')
  arr[0] = arr[0].split('_vs_').flatten
  puts `cd ..; ./preprocess.sh RY_log.dat #{arr.join ' '}`
  figname = d.gsub(/\//, '-') + '.png'
  puts `cp ../Fig.png #{d}/#{figname}`
end

dirs = Dir.glob('*/*')

dirs.each do |d|
  file = "#{d}/RY_log.dat"
  if File.exist?(file)
    do_whats_necessary(file, d)
  else
    alt_file = "#{d}/RY_Log.dat"
    if File.exist?(alt_file)
      do_whats_necessary(alt_file, d)
    else
      puts "ERROR: file #{file} not found!"
    end
  end
end
