Sections = {0, 0, 0, 0, 0, 0, 0, 0, 0}
Player = 1

function Printgame(array)
    local newline = 0
    for i, value in ipairs(array) do
        newline = newline + 1
        if value == 0 then io.write(". ")
        elseif value == 1 then io.write("o ")
        elseif value == 2 then io.write("x ") end

        if newline % 3 == 0 then print() end
    end
end

function Playerenter(array, player)
    local enter = tonumber(io.read())
    if array[enter] == 0 then
        array[enter] = player
        return true, array
    else return false end
end

function Changeplayer(player)
    if player == 1 then return 2
    else return 1 end
end

function Checkwin(array)
    local winningcombinations = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}, {1, 4, 7}, {2, 5, 8}, {3, 6, 9}, {1, 5, 9}, {3, 5, 7}}
    for i, combination in ipairs(winningcombinations) do
        if array[combination[1]] == array[combination[2]] and array[combination[2]] == array[combination[3]] and array[combination[1]] ~= 0 then
            return array[combination[1]]
        end
    end
end

while true do
    ::continue::
    Printgame(Sections)
    local free, newarray = Playerenter(Sections, Player)
    if free then Sections = newarray
    else goto continue end
    Player = Changeplayer(Player)
    if Checkwin(Sections) ~= nil then
        Printgame(Sections)
        print (Checkwin(Sections))
        local winner = Checkwin(Sections)
        print("Player " .. winner .. " win!\n")
        break
    end
end
