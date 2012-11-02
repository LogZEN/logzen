
map = (data, transform_key, transform_value) ->
  result = {}
  
  for key, value of data
    result[transform_key key] = transform_value value
  
  return result
  


generate = (template) ->
  if template instanceof Function
    generate template()
    
  else if template instanceof Array 
    generate e for e in template
    
  else if template instanceof Object
    map template, ((key) -> generate key), ((value) -> generate value)
  
  else
    template



cs = (template) ->
  ###
  Creates new construct.js template.
  
  The passed template is a structure containing a valid JSON structure
  additionally allow functions as values.
  
  If the generator is called, the template will manifested into a JSON strucutre
  by resolving the functions.
  ###
  generator = () ->
    generate generator.template
    
  generator.template = template
  
  return generator



cs.if = (condition, a, b) ->
  ###
  Generator for a condition.
  
  The condition will be evaluated and if the condition evaluates to true, the a
  value will be returned, otherwise the b value will be returned.
  ###
  () -> if generate condition then generate a else generate b



cs.filter = (predicate, data) ->
  ###
  Filters a structure.
  
  The structure is filtered using the given predicate. The predicate must be a
  function getting the resolved key and the resolved value as a parameters. The
  return value must be a boolean. If the return value is true, the value will be
  stored under the key in the resulting map. If the return value is false, the
  key - value pair will be left out.
  ###
  () ->
    result = {}
    for key, value of generate data
      if predicate key, value
        result[key] = value
    
    return result




@cs = cs
