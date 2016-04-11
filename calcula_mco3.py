# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# calcula_mco3.py
# Created on: 2016-02-11
# Description: calculo de la MÁXIMA CRECIDA ORDINARIA (MCO) mediante mediante la
# función de distribución de Valores Extremos Generalizada y el método de mínimos cuadrados.
# ---------------------------------------------------------------------------
# proyecto: PROTOCOLO DE CARACTERIZACI?N HIDROMORFOL?GICA DE MASAS DE AGUA.
#
# Obtencion de par?metros:
# dQ: valores de caudales para los periodos de retorno de 2,5,10,25,100y500 años
#
# Author:      JESUS GARCÍA VILLAR
#	web : servigis.com
# Created:     11/04/2016
# Copyright:   (c) JESUS 2015
#-------------------------------------------------------------------------------


import sys,math

def main():
    pass

if __name__ == '__main__':
    main()


try:
    import arcpy, os, sys, traceback,numpy,numbers
    #import tkinter
    from arcpy import env

    arcpy.env.overwriteOutput = True

    capa = r"C:/tmp/caumax.mdb/tajo"
    item = "mco"
    env.workspace = capa
    rows = arcpy.UpdateCursor(capa)
    desc = arcpy.Describe(capa)
    count = int(arcpy.GetCount_management(capa).getOutput(0))

    def my_range1(start, end, step):
               while start < end:
                              yield start
                              start += step

    def my_range2(start, end, step):
               while start < end:
                              yield start
                              start += step

    def my_range3(start, end, step):
               while start < end:
                              yield start
                              start += step

    def getSquaredDiff(dA,  dU,  dK, dQ):
        dDif = 0;
    	dSum = 0;
        m_dF = [0.5,0.8,0.9,0.96,0.99,0.998];
        for i in range(0,len(m_dF)):
			#ley de frecuencias
			d= dU + dA / dK * (1- math.pow(-math.log(m_dF[i]), dK))
			dDif = d - dQ[i]
			dSum += (dDif*dDif)

        return dSum;

    def interpolacion(dQ):
        dLimit = (dQ[1] + dQ[4])/ 4.
    	dInterval = dLimit / 100
       	dMinDiff=  sys.float_info.max

        dAlpha = 0
        dMu = 0
        dK = -0.5
        cuentadAlpha = 0
        cuentadK = 0
        cuentadMu = 0
    	for vdAlpha in my_range1(dAlpha ,  dLimit, dAlpha + dInterval):
            cuentadAlpha  = cuentadAlpha + 1
            for vdMu in my_range2(dMu , dLimit, dMu + dInterval):
                cuentadMu  = cuentadMu + 1
                for vdK in my_range3(-0.5 , 0 , 0.01):
                    cuentadK  = cuentadK + 1
                    dDiff = getSquaredDiff(vdAlpha, vdMu, vdK, dQ)
                    if dDiff < dMinDiff:
    					dMinDiff = dDiff
    					m_dAlpha = vdAlpha
    					m_dMu = vdMu
    					m_dK = vdK
    					m_dSumOfSquares = dDiff
        return (m_dAlpha,m_dMu,m_dK)

    n = 0

    for row in rows:
      n = n + 1
      dQ = [row.q2, row.q5, row.q10, row.q25, row.q100, row.q500]
      ti = row.T_MCO
      #valor = row.q2 + row.q5
      tmp = interpolacion(dQ)

      valorm_dAlpha = tmp[0]
      valor_m_dMu = tmp[1]
      valor_m_dK = tmp[2]
      valor = valor_m_dMu + valorm_dAlpha / valor_m_dK * (1 - math.pow(-math.log((1 - 1. / ti)), valor_m_dK))

      #valor = tmp.m_dMu + tmp.m_dAlpha / tmp.m_dK * (1 - Math.pow(-Math.log((1 - 1. / ti)), tmp.m_dK))
##      print valores[0]
##      print valores[1]
##      q2 = ' "%s"' % (valor,)
      row.setValue("mco", valor)
      rows.updateRow(row)
      #arcpy.CalculateField_management(capa,"mco",valor,"PYTHON")
      #print (capa, "mco",valor,"PYTHON")
      #print ("Q = " + str(valor)+" valorm_dAlpha = " + str(valorm_dAlpha)+ "  valor_m_dMu = " + str(valor_m_dMu)+ "  valor_m_dK = " + str(valor_m_dK))
      print (" procesando " + str(n) + " de " + str(count))
      #print ("Q = " + str(valor)+"  t_mco = "+ str(ti)+"  "+ "Q 2 5 10 25 100 500 = " + str(dQ[0])+"- "+str(dQ[1])+ "-"+str(dQ[2])+"-"+ str(dQ[3])+"-"+ str(dQ[4])+"-"+ str(dQ[5]) + " valorm_dAlpha = " + str(valorm_dAlpha)+ "  valor_m_dMu = " + str(valor_m_dMu)+ "  valor_m_dK = " + str(valor_m_dK))


except:
        # Get the traceback object
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + \
                "\nError Info:\n" + str(sys.exc_info()[1])
        msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
        arcpy.AddError(pymsg)
        arcpy.AddError(msgs)

        # Print Python error messages for use in Python / Python Window
        print pymsg + "\n"
        print msgs