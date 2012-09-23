#!/usr/bin/env ruby

require './constraints'

f = File.open("czyste.dat","rt")
names_arr = f.gets.split

raise "Incorrect argument count: provide at least x y z + constraints" unless ARGV.count > 3

columns, constraints = Constraint.parse_args(ARGV, names_arr)
p columns
p constraints
puts "\n------------------------"
columns.each do |c|
  puts "#{c}: #{names_arr[c]}"
end

#Write results to file
out = File.open("dane_tmp.dat","wt")

header_arr = columns.map{|c| names_arr[c]}
out.puts header_arr.join("\t")

f.each_line do |line|
  values = columns.map{ |c| line.split[c] }
  constr_ok = true
  constraints.each { |constraint|
   constr_ok &= constraint.fulfilled?(values, header_arr)
  }
  out.puts values.join("\t") if constr_ok
end
