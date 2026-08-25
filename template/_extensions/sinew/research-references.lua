local function argument_text(args, shortcode)
  if #args ~= 1 then
    error("The " .. shortcode .. " shortcode expects exactly one argument.")
  end
  return pandoc.utils.stringify(args[1])
end

local function statement_reference(kind, prefix, args)
  local value = argument_text(args, string.lower(prefix))
  local number = tonumber(value)
  if number == nil or number % 1 ~= 0 or number < 1 or number > 9 then
    error("Research references must use an integer from 1 through 9.")
  end

  local label = prefix .. tostring(number)
  local attributes = {
    {"data-sinew-reference-kind", kind},
    {"data-sinew-reference-number", tostring(number)}
  }
  local classes = {
    "sinew-reference",
    "sinew-statement-reference",
    "sinew-reference-" .. kind
  }
  return pandoc.Link({pandoc.Str(label)}, "#", "", pandoc.Attr("", classes, attributes))
end

local function algorithm_reference(args)
  local target = argument_text(args, "alg")
  if not target:match("^algorithm%-%l[%l%d%-]*$") then
    error("The alg shortcode target must start with algorithm- and use lowercase ASCII letters, digits, and hyphens.")
  end

  local attributes = {
    {"data-sinew-reference-kind", "algorithm"},
    {"data-sinew-reference-target", target}
  }
  local classes = {
    "sinew-reference",
    "sinew-algorithm-reference"
  }
  return pandoc.Link({pandoc.Str("Algorithm")}, "#", "", pandoc.Attr("", classes, attributes))
end

return {
  ["q"] = function(args)
    return statement_reference("question", "Q", args)
  end,
  ["h"] = function(args)
    return statement_reference("hypothesis", "H", args)
  end,
  ["alg"] = function(args)
    return algorithm_reference(args)
  end
}
