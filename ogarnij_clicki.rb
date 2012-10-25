#!/usr/bin/env ruby

require './constraints'

params = %w(phi charge diam Salt alpha)

fh = File.open("last_choice", "rt")
constr_string = fh.gets.split
constr_string.delete_at 2 # ingore the z axis
columns, constraints = Constraint.parse_args(constr_string, params)

p constraints
puts

fdata = File.open("clicks.dat", "rt")
xh, yh, ah = fdata.gets.strip.split("\t")
print "Data file header: #{xh}, #{yh}, #{ah}"

fout = File.open("batch.dat", "wt")
fout.puts params.join("\t")

fdata.each do |line|
  values = line.split
  hash = {xh => values[0], yh => values[1], ah => values[2]}
  constraints.each do |c|
    hash[c.name] = c.value
  end
  puts hash
  fout.puts params.map{ |p| hash[p] }.join("\t")
end
