#!/usr/bin/env ruby

def within(a,b,e)
  ((a.to_f-b.to_f)/a.to_f).abs < e.to_f
end

avg = true if ARGV.count > 2 && ARGV[2] == "--avg"
raise "check_dups INFILE OUTFILE [--avg]" unless [2,3].include? ARGV.count

f = open(ARGV[0], 'rt')
header = f.gets
eps = 0.01
data = {}

f.each_line do |l|
  arr = l.split.map{|x| x.to_f}
  xy = arr[0..1]
  if data.keys.include? xy
    unless within(arr[2], data[xy][0], eps)
      puts "Duplicate: #{xy}:  #{arr[2]} vs #{data[xy][0]}"
      if avg
        data[xy][0] = (data[xy][0] + arr[2]) / 2
        puts "Averaged: #{data[xy][0]}"
      end
    end
  end

  data[xy] = [arr[2], arr[3..-1]]
end

f.close

f = open(ARGV[1], 'wt')
f.puts header
data.each { |k,v| f.puts k.join("\t")+"\t"+v.join("\t") }

