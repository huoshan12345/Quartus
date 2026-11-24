library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity memory4096x16 is
    port (
        CLK : in std_logic;
        READ_EN, WRITE_EN : in std_logic;
        ADDRESS : in std_logic_vector(11 downto 0);
        DATA : in std_logic_vector(15 downto 0);
        Q : out std_logic_vector(15 downto 0)
    );
end entity;

architecture rtl of memory4096x16 is
    type memory_array is array (0 to 4095) of std_logic_vector(15 downto 0);
    signal ram : memory_array;
begin
    -- Basic-computer memory interface: synchronous write, combinational read.
    -- No program image is assumed; initialize RAM explicitly before execution.
    process (CLK)
    begin
        if rising_edge(CLK) then
            if WRITE_EN = '1' then
                ram(to_integer(unsigned(ADDRESS))) <= DATA;
            end if;
        end if;
    end process;
    Q <= ram(to_integer(unsigned(ADDRESS))) when READ_EN = '1'
         else (others => '0');
end architecture;
