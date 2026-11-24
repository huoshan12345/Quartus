-- Dual-port on-chip RAM (4096 x 16-bit) configured per Assignment #3 Memory selection.pdf:
-- One write port (wrclock = system CLK) and one read port (rdclock = inverted CLK),
-- unregistered read output q, initialized from program.mif.

LIBRARY ieee;
USE ieee.std_logic_1164.all;

LIBRARY altera_mf;
USE altera_mf.altera_mf_components.all;

ENTITY ram2port IS
    PORT
    (
        data      : IN  STD_LOGIC_VECTOR (15 DOWNTO 0);
        rdaddress : IN  STD_LOGIC_VECTOR (11 DOWNTO 0);
        rdclock   : IN  STD_LOGIC;
        wraddress : IN  STD_LOGIC_VECTOR (11 DOWNTO 0);
        wrclock   : IN  STD_LOGIC := '1';
        wren      : IN  STD_LOGIC := '0';
        q         : OUT STD_LOGIC_VECTOR (15 DOWNTO 0)
    );
END ram2port;

ARCHITECTURE SYN OF ram2port IS
    SIGNAL sub_wire0 : STD_LOGIC_VECTOR (15 DOWNTO 0);
BEGIN
    q <= sub_wire0(15 DOWNTO 0);

    altsyncram_component : altsyncram
    GENERIC MAP (
        address_aclr_b               => "NONE",
        address_reg_b                => "CLOCK1",
        clock_enable_input_a         => "BYPASS",
        clock_enable_input_b         => "BYPASS",
        clock_enable_output_b        => "BYPASS",
        init_file                    => "program.mif",
        init_file_layout             => "PORT_B",
        intended_device_family       => "Cyclone V",
        lpm_type                     => "altsyncram",
        numwords_a                   => 4096,
        numwords_b                   => 4096,
        operation_mode               => "DUAL_PORT",
        outdata_aclr_b               => "NONE",
        outdata_reg_b                => "UNREGISTERED",
        power_up_uninitialized       => "FALSE",
        ram_block_type               => "AUTO",
        widthad_a                    => 12,
        widthad_b                    => 12,
        width_a                      => 16,
        width_b                      => 16,
        width_byteena_a              => 1
    )
    PORT MAP (
        address_a => wraddress,
        address_b => rdaddress,
        clock0    => wrclock,
        clock1    => rdclock,
        data_a    => data,
        wren_a    => wren,
        q_b       => sub_wire0
    );
END SYN;
