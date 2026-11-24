-- Testbench for Assignment #3 Basic Computer (ECE 6500 / ENGI 9861)
-- Executes the program stored in program.mif and monitors AC, E, S,
-- and the affected memory locations M[103] and M[201].

LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;

ENTITY tb_basic_computer IS
END ENTITY tb_basic_computer;

ARCHITECTURE sim OF tb_basic_computer IS
    COMPONENT basic_computer IS
        PORT (
            MEM_WR_OUT  : OUT std_logic;
            CLK         : IN  std_logic;
            RESET       : IN  std_logic;
            AC_Q        : OUT std_logic_vector(15 DOWNTO 0);
            INPUT_DATA  : IN  std_logic_vector(7 DOWNTO 0);
            DR_Q        : OUT std_logic_vector(15 DOWNTO 0);
            FLAG_Q      : OUT std_logic_vector(6 DOWNTO 0);
            IR_Q        : OUT std_logic_vector(15 DOWNTO 0);
            E_OUT       : OUT std_logic;
            S_OUT       : OUT std_logic;
            AR_Q        : OUT std_logic_vector(11 DOWNTO 0);
            BUS_DATA    : OUT std_logic_vector(15 DOWNTO 0);
            MEM_Q       : OUT std_logic_vector(15 DOWNTO 0);
            OUTPUT_DATA : OUT std_logic_vector(7 DOWNTO 0);
            PC_Q        : OUT std_logic_vector(11 DOWNTO 0);
            SC_Q        : OUT std_logic_vector(3 DOWNTO 0)
        );
    END COMPONENT;

    CONSTANT CLK_PERIOD : time := 20 ns;

    SIGNAL clk         : std_logic := '0';
    SIGNAL reset       : std_logic := '1';
    SIGNAL input_data  : std_logic_vector(7 DOWNTO 0) := (others => '0');

    SIGNAL ac_q        : std_logic_vector(15 DOWNTO 0);
    SIGNAL e_out       : std_logic;
    SIGNAL s_out       : std_logic;
    SIGNAL pc_q        : std_logic_vector(11 DOWNTO 0);
    SIGNAL ar_q        : std_logic_vector(11 DOWNTO 0);
    SIGNAL ir_q        : std_logic_vector(15 DOWNTO 0);
    SIGNAL dr_q        : std_logic_vector(15 DOWNTO 0);
    SIGNAL bus_data    : std_logic_vector(15 DOWNTO 0);
    SIGNAL mem_q       : std_logic_vector(15 DOWNTO 0);
    SIGNAL mem_wr_out  : std_logic;
    SIGNAL sc_q        : std_logic_vector(3 DOWNTO 0);
    SIGNAL flag_q      : std_logic_vector(6 DOWNTO 0);
    SIGNAL output_data : std_logic_vector(7 DOWNTO 0);

    -- Live monitors for the memory locations written by the test program.
    SIGNAL mem_103     : std_logic_vector(15 DOWNTO 0) := x"0000";
    SIGNAL mem_201     : std_logic_vector(15 DOWNTO 0) := x"0000";
    SIGNAL sim_done    : boolean := false;

    FUNCTION to_hex(v : std_logic_vector) RETURN string IS
        CONSTANT hex_chars : string(1 TO 16) := "0123456789ABCDEF";
        VARIABLE n   : integer := v'length / 4;
        VARIABLE res : string(1 TO v'length / 4);
        VARIABLE nib : std_logic_vector(3 DOWNTO 0);
        VARIABLE u   : unsigned(v'length - 1 DOWNTO 0) := unsigned(v);
    BEGIN
        FOR i IN 0 TO n - 1 LOOP
            nib := std_logic_vector(u(v'length - 1 - 4 * i DOWNTO v'length - 4 - 4 * i));
            IF is_x(nib) THEN
                res(i + 1) := 'X';
            ELSE
                res(i + 1) := hex_chars(to_integer(unsigned(nib)) + 1);
            END IF;
        END LOOP;
        RETURN res;
    END FUNCTION;
BEGIN
    uut : basic_computer
        PORT MAP (
            MEM_WR_OUT  => mem_wr_out,
            CLK         => clk,
            RESET       => reset,
            AC_Q        => ac_q,
            INPUT_DATA  => input_data,
            DR_Q        => dr_q,
            FLAG_Q      => flag_q,
            IR_Q        => ir_q,
            E_OUT       => e_out,
            S_OUT       => s_out,
            AR_Q        => ar_q,
            BUS_DATA    => bus_data,
            MEM_Q       => mem_q,
            OUTPUT_DATA => output_data,
            PC_Q        => pc_q,
            SC_Q        => sc_q
        );

    -- System clock generator (50 MHz, 20 ns period).
    clk_proc : PROCESS
    BEGIN
        WHILE NOT sim_done LOOP
            clk <= '0';
            WAIT FOR CLK_PERIOD / 2;
            clk <= '1';
            WAIT FOR CLK_PERIOD / 2;
        END LOOP;
        WAIT;
    END PROCESS;

    -- Track memory writes to M[103] and M[201] (and log every memory write).
    mem_mon_proc : PROCESS (clk)
    BEGIN
        IF rising_edge(clk) THEN
            IF reset = '1' THEN
                mem_103 <= x"0000";
                mem_201 <= x"0000";
            ELSIF mem_wr_out = '1' THEN
                REPORT "MEM WRITE at " & time'image(now) &
                       ": M[" & to_hex(ar_q) & "] <= " & to_hex(bus_data);
                IF ar_q = x"103" THEN
                    mem_103 <= bus_data;
                ELSIF ar_q = x"201" THEN
                    mem_201 <= bus_data;
                END IF;
            END IF;
        END IF;
    END PROCESS;

    -- Stimulus and verification sequence.
    stim_proc : PROCESS
        VARIABLE cycle_cnt : integer := 0;
    BEGIN
        -- Synchronous reset for 2 rising clock edges.
        reset <= '1';
        WAIT FOR 2 * CLK_PERIOD;
        WAIT UNTIL falling_edge(clk);
        reset <= '0';

        -- Run until HLT (S_OUT = '0') or safety timeout.
        WHILE cycle_cnt < 100 LOOP
            WAIT UNTIL rising_edge(clk);
            WAIT FOR 2 ns;
            cycle_cnt := cycle_cnt + 1;
            REPORT "Cycle " & integer'image(cycle_cnt) &
                   " | SC=" & to_hex(sc_q) &
                   " PC=" & to_hex(pc_q) &
                   " AR=" & to_hex(ar_q) &
                   " IR=" & to_hex(ir_q) &
                   " DR=" & to_hex(dr_q) &
                   " AC=" & to_hex(ac_q) &
                   " E=" & std_logic'image(e_out) &
                   " S=" & std_logic'image(s_out) &
                   " M103=" & to_hex(mem_103) &
                   " M201=" & to_hex(mem_201);
            IF s_out = '0' THEN
                EXIT;
            END IF;
        END LOOP;

        -- Hold a few extra cycles after HLT to prove machine remains halted.
        WAIT FOR 4 * CLK_PERIOD;

        ASSERT s_out = '0'
            REPORT "FAIL: CPU did not halt (S_OUT /= '0')." SEVERITY error;
        ASSERT ac_q = x"CEFE"
            REPORT "FAIL: Expected AC = CEFE, got " & to_hex(ac_q) SEVERITY error;
        ASSERT e_out = '1'
            REPORT "FAIL: Expected E = '1' after CME, got " & std_logic'image(e_out) SEVERITY error;
        ASSERT mem_103 = x"0102"
            REPORT "FAIL: Expected M[103] = 0102, got " & to_hex(mem_103) SEVERITY error;
        ASSERT mem_201 = x"CEFE"
            REPORT "FAIL: Expected M[201] = CEFE, got " & to_hex(mem_201) SEVERITY error;

        REPORT "PASS: Basic Computer halted cleanly with AC=" & to_hex(ac_q) &
               ", E=" & std_logic'image(e_out) &
               ", M[103]=" & to_hex(mem_103) &
               ", M[201]=" & to_hex(mem_201) & ".";

        sim_done <= true;
        WAIT;
    END PROCESS;
END ARCHITECTURE sim;
