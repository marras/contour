#!/usr/bin/env ruby

class Constraint
  def initialize(str, name)
    raise "Incorrect constraint format!" unless str =~ /=/
    @name = name
    @rhs = str.split('=')[1]
    if @rhs =~ /,/
      @min, @max = @rhs.split(',')
      if @max < @min
        @min, @max = @max, @min
      end
    end
  end

  def fulfilled?(arr, header)
    index = header.find_index(@name)
    if index.nil?
      raise "Constraint#fulfilled?: Column not found with name #{@name}!"
    end

    if @rhs =~ /,/
      return arr[index].to_f >= @min.to_f && arr[index].to_f <= @max.to_f
    elsif @rhs == '*'
      return true
    elsif @rhs[0] == '~' # =~ --> 10% uncertainty
      rhs_value = @rhs[1..-1].to_f
      return arr[index].to_f >= rhs_value / 1.1 && arr[index].to_f <= rhs_value * 1.1
    else
      return arr[index] == @rhs
    end
  end
end

f = File.open("czyste.dat","rt")
arr = f.gets.split
columns = []
fields = []
constraints = []

raise "Incorrect argument count: provide at least x y z + constraints" unless ARGV.count > 3

# Find the correct columns by regexp search
ARGV.each do |arg|
  if arg =~ /=/
    regex = Regexp.new(arg.split('=')[0], Regexp::IGNORECASE)
  else
    regex = Regexp.new(arg, Regexp::IGNORECASE)
  end

  max_score = 0
  max_index = 0
  arr.each do |e|
    if m = regex.match(e)
      score = m.to_s.size.to_f / e.size.to_f
      puts "#{e}: #{m}, #{score}"
      if score > max_score
        max_index = arr.find_index(e)
        max_score = score
      end
    end
  end
  columns << max_index
  constraints << Constraint.new(arg, arr[max_index]) if arg =~ /=/ 

  raise "No column found for /#{arg}/" unless max_score > 0
end

puts "\n------------------------"
columns.each do |c|
  puts "#{c}: #{arr[c]}"
end

#Write results to file
out = File.open("dane_tmp.dat","wt")

header_arr = columns.map{|c| arr[c]}
out.puts header_arr.join("\t")

f.each_line do |line|
  arr = columns.map{ |c| line.split[c] }
  constr_ok = true
  constraints.each { |constraint|
   constr_ok &= constraint.fulfilled?(arr, header_arr)
  }
  out.puts arr.join("\t") if constr_ok
end
