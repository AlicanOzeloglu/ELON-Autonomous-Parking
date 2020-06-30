----------------------------------------------------------------------------------
-- Engineer: Mike Field <hamster@snap.net.nz>
--
-- Description: Captures the pixels coming from the OV7670 camera and
--              Stores them in block RAM
----------------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.ALL;
use ieee.NUMERIC_STD.ALL;

entity ov7670_capture is
    port (
        pclk  : in   std_logic;
        vsync : in   std_logic;
        href  : in   std_logic;
        d     : in   std_logic_vector ( 7 downto 0);
        addr  : out  std_logic_vector (18 downto 0);
        dout  : out  std_logic_vector (11 downto 0);
        we    : out  std_logic;
        red_detection : out std_logic;
        detect_out : out std_logic
    );
end ov7670_capture;

architecture behavioral of ov7670_capture is
   signal d_latch      : std_logic_vector(15 downto 0) := (others => '0');
   signal address      : std_logic_vector(18 downto 0) := (others => '0');
   signal address_next : std_logic_vector(18 downto 0) := (others => '0');
   signal wr_hold      : std_logic_vector( 1 downto 0)  := (others => '0');
   signal counter      : unsigned(15 downto 0);
   --signal detect_sig_current   : std_logic :='0';
   --signal detect_sig_prev   : std_logic :='0';
   signal detect_sig   : std_logic :='0';
   signal detect_catch   : std_logic :='0';

begin
   --addr <= address(18 downto 1);
   addr <= address;
   process(pclk)
   begin
      if falling_edge(pclk) then
         -- This is a bit tricky href starts a pixel transfer that takes 3 cycles
         --        Input   | state after clock tick
         --         href   | wr_hold    d_latch           d                 we address  address_next
         -- cycle -1  x    |    xx      xxxxxxxxxxxxxxxx  xxxxxxxxxxxxxxxx  x   xxxx     xxxx
         -- cycle 0   1    |    x1      xxxxxxxxRRRRRGGG  xxxxxxxxxxxxxxxx  x   xxxx     addr
         -- cycle 1   0    |    10      RRRRRGGGGGGBBBBB  xxxxxxxxRRRRRGGG  x   addr     addr
         -- cycle 2   x    |    0x      GGGBBBBBxxxxxxxx  RRRRRGGGGGGBBBBB  1   addr     addr+1

         if vsync = '1' then
            address <= (others => '0');
            address_next <= (others => '0');
            wr_hold <= (others => '0');
         else
            -- This should be a different order, but seems to be GRB!
            dout    <= d_latch(15 downto 12) & d_latch(10 downto 7) & d_latch(4 downto 1);
            address <= address_next;
            we      <= wr_hold(1);
            wr_hold <= wr_hold(0) & (href and not wr_hold(0));
            d_latch <= d_latch( 7 downto  0) & d;

            if wr_hold(1) = '1' then
               address_next <= std_logic_vector(unsigned(address_next)+1);
            end if;
         end if;
      end if;
   end process;
   process(pclk)
    begin
     if falling_edge(pclk) then
        if wr_hold(1) = '1' and  unsigned(d_latch(15 downto 12)) > 12 and unsigned(d_latch(10 downto 7)) < 4 and unsigned(d_latch(4 downto 1)) < 4 then
            red_detection <= '1';
            detect_sig <= '1';
        else
            detect_sig <= '0';
            red_detection <= '0';
        end if;
     end if;
  end process;
  
--  process(pclk)
--  begin
--   if falling_edge(pclk) then
--      if detect_sig_current = '1' then
--          detect_sig_prev <= '1';
--      else
--          detect_sig_prev <= '0';
--      end if;
--      if detect_sig_current = '1' and  detect_sig_prev = '1' then
--            detect_sig <= '1';
--        else
--            detect_sig <= '0';
--        end if;
--   end if;
--end process;
  
   process(pclk)
   begin
      if falling_edge(pclk) then
         if (detect_sig = '1' or detect_catch = '1') and counter < 100 then
            detect_catch <= '1';
            detect_out <= '1';
            counter <= counter + 1;
         else
             detect_out <= '0';
            detect_catch <= '0';
            counter <= (others => '0');
         end if;
      end if;
   end process;
  
   
end behavioral;