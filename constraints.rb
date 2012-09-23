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

  def fulfilled?(names, header)
    index = header.find_index(@name)
    if index.nil?
      raise "Constraint#fulfilled?: Column not found with name #{@name}!"
    end

    if @rhs =~ /,/
      return names[index].to_f >= @min.to_f && names[index].to_f <= @max.to_f
    elsif @rhs == '*'
      return true
    elsif @rhs[0] == '~' # =~ --> 10% uncertainty
      rhs_value = @rhs[1..-1].to_f
      return names[index].to_f >= rhs_value / 1.1 && names[index].to_f <= rhs_value * 1.1
    else
      return names[index].to_f == @rhs.to_f
    end
  end

  def value
    if @rhs =~ /,/
      print "Warning: called value() for a range-based Constraint"
      (@min + @max) / 2
    elsif @rhs == '*'
      raise "Error: constraint value defined as 'any' (*)"
    elsif @rhs[0] == '~' # =~ --> 10% uncertainty
      @rhs[1..-1].to_f
    else
      @rhs.to_f
    end
  end

  # Find the correct columns by regexp search
  def self.parse_args(constraints_string, names_arr)
    columns = []
    fields = []
    constraints = []

    puts "Constraints detection:"

    constraints_string.each do |arg|
      if arg =~ /=/
        regex = Regexp.new(arg.split('=')[0], Regexp::IGNORECASE)
      else
        regex = Regexp.new(arg, Regexp::IGNORECASE)
      end

      max_score = 0
      max_index = 0
      names_arr.each do |e|
        if m = regex.match(e)
          score = m.to_s.size.to_f / e.size.to_f
          puts "#{e}: #{m}, #{score}"
          if score > max_score
            max_index = names_arr.find_index(e)
            max_score = score
          end
        end
      end
      columns << max_index
      constraints << Constraint.new(arg, names_arr[max_index]) if arg =~ /=/ 

      raise "No column found for /#{arg}/" unless max_score > 0
    end

    return columns, constraints
  end
end
