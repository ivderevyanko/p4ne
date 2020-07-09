- hosts: fs-ga
  tasks:
   - name: show interfaces
     command: ifconfig -a
     register: ifconfig

   - name:
     set_fact:
         packets: "{{ interfaces['stdout'] | regex_findall('RX packets:([0-9]+)') }}"

   - name: show results
     debug:
         msg: "{{ packets | map('int') | sum }}"