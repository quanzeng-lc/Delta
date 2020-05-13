#!/usr/env/bin python3
# -*- coding:utf-8 -*-
from SensorI import SensorI
from SensorO import SensorO

class SensorsMgr:
    def __init__(self):
        self.i_size = 12
        self.o_size = 3
        self.started = False
        self.io_in = list[self.i_size]
        self.io_out = list[self.o_size]

        for i_num in range(0, self.i_size):
            self.io_in[i_num] = SensorI(i_num)

        for o_num in range(0, self.o_size):
           self.io_out[i_num] = SensorO(i_num)

        workthreadI = new Thread(WorkMethodI);
        workthreadI.IsBackground = true;
        workthreadO = new Thread(WorkMethodO);
        workthreadO.IsBackground = true
        workthreadI.Priority = ThreadPriority.Highest
        workthreadO.Priority = ThreadPriority.Highest
        started = false;

    def set_gpo(self, no, val):
        value = (ushort)(val == 0 ? 1: 0);
        if no >= 0 and no <= 15:
            DMC3000.dmc_write_outbit(0, (ushort)no, value)
        elif no >= 16 and no <= 31:
            DMC3000.dmc_write_outbit(1, (ushort)(no - 16), value);
        elif no >= -1 and no < 64:
            ret = IOC0640.ioc_write_outbit(0, (ushort)(no + 1), value);


    def get_sensor_i(self, no):
        if no < 0 or no > self.i_size:
            return null
        return self.io_in[no]

    def get_sensor_o(self, no):
        if no < 0 or no > self.o_size:
            return None
        return self.io_in[no]

    def get_dmc3000_i(self):
        # 普通IO信号
        for ushort i = 0; i < 2; i++:
            vals = DMC3000.dmc_read_inport(i, 0);
            for (int j = 0; j < 4; j++)
                uint val = (uint)(1 << j)
            if (vals and val) == val:
                IO_IN[194 + i * 4 + j].UpdateVal(1)
            else:
            IO_IN[194 + i * 4 + j].UpdateVal(0);

        # 轴状态
        # 伺服报警、正硬极限、负硬极限、原点、正软限位、负软限位
        int[] pos = {0, 1, 2, 4, 6, 7};
        for (ushort i = 0; i < 21; i++)
            vals = Aixs[i].AxisIoStatus();
            for (var j = 0; j < 6; j++)
                uint val = (uint)1 << pos[j];
            if ((vals & val) == val)
                IO_IN[i * 6 + j + 64].UpdateVal(1);
            else
                IO_IN[i * 6 + j + 64].UpdateVal(0);

    def get_gcn800a_gpi(self):
        # 普通IO信号
        for (ushort i = 0; i < GCN800A.pDevHandleArrayLength; i++)
            vals = GCN800A.dmc_read_inport(i, 0);
            for (int j = 0; j < 4; j++)
                uint val = (uint)(1 << j);
            if ((vals & val) == val)
                IO_IN[194 + i * 4 + j].UpdateVal(1);
            else
            IO_IN[194 + i * 4 + j].UpdateVal(0);


    def get_ioc0640_i(self):
        for (ushort i = 0; i < 2; i++)
            vals = IOC0640.ioc_read_inport(0, i);
        for (int j = 0; j < 32; j++)
            uint val = (uint)1 << j;
        if ((vals & val) == val)
            IO_IN[i * 32 + j].UpdateVal(0);
        else
            IO_IN[i * 32 + j].UpdateVal(1);


    # 虚拟IO 190~193
    def get_vir_i(self):
        if (IO_IN[16].GetVal() & & IO_IN[17].GetVal())
            IO_IN[190].UpdateVal(1);
        else
            IO_IN[190].UpdateVal(0);
        if (IO_IN[18].GetVal() & & IO_IN[19].GetVal())
            IO_IN[191].UpdateVal(1);
        else
            IO_IN[191].UpdateVal(0);
        if (RelayMgr.GetVal("Pause") == 1)
            IO_IN[192].UpdateVal(1);
        else
            IO_IN[192].UpdateVal(0);
        if (IO_IN[47].GetVal() & & IO_IN[48].GetVal() & & IO_IN[49].GetVal() & & IO_IN[50].GetVal())
            IO_IN[193].UpdateVal(0);
        else
            IO_IN[193].UpdateVal(1);

    def clear(self):
        for i = 0; i < I_SIZE; i++
            IO_IN[i].Clear()

        for int i = 0; i < O_SIZE; i++
            IO_OUT[i].Clear()

    def start(self):
        if !started :
            started = true;
            Clear();
            workthreadI.Priority = ThreadPriority.AboveNormal
            workthreadO.Priority = ThreadPriority.AboveNormal
            workthreadI.Start()
            workthreadO.Start()

    def Stop(self):
        if started:
            started = false
            workthreadI = new Thread(WorkMethodI)
            workthreadI.IsBackground = true
            workthreadO = new Thread(WorkMethodO)
            workthreadO.IsBackground = true
            workthreadI.Priority = ThreadPriority.Highest
            workthreadO.Priority = ThreadPriority.Highest

    def WorkMethodI(self):
        while started:
            GetIOC0640_I()
            GetDMC3000_I()
            GetVir_I()
            for (int i = 0; i < I_SIZE; i++)
                IO_IN[i].DoWork()
            Thread.Sleep(1)

    def WorkMethodO(self):
        while started:
            GetIOC0640_O()
            for (int i = 0; i < O_SIZE; i++)
                IO_OUT[i].DoWork()
            Thread.Sleep(1)
