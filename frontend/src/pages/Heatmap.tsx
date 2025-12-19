import React, { useState } from 'react';
import { Layout } from '@/components/layout/Layout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { mockCases, districts } from '@/data/mockCases';
import { Map, Filter, TrendingUp, AlertTriangle } from 'lucide-react';

interface HeatmapCell {
  district: string;
  count: number;
  lat: number;
  lng: number;
}

const Heatmap: React.FC = () => {
  const [selectedDistrict, setSelectedDistrict] = useState<string>('');
  const [timeFilter, setTimeFilter] = useState<string>('all');

  // Calculate case counts by district
  const districtCounts: HeatmapCell[] = districts.map((district) => {
    const cases = mockCases.filter((c) => c.district === district);
    const avgLat = cases.length > 0
      ? cases.reduce((sum, c) => sum + c.latitude, 0) / cases.length
      : 28.6139;
    const avgLng = cases.length > 0
      ? cases.reduce((sum, c) => sum + c.longitude, 0) / cases.length
      : 77.209;
    return {
      district,
      count: cases.length,
      lat: avgLat,
      lng: avgLng,
    };
  }).filter((d) => d.count > 0);

  const maxCount = Math.max(...districtCounts.map((d) => d.count));

  const getHeatColor = (count: number) => {
    const intensity = count / maxCount;
    if (intensity > 0.7) return 'bg-destructive';
    if (intensity > 0.4) return 'bg-warning';
    return 'bg-success';
  };

  const selectedDistrictData = districtCounts.find((d) => d.district === selectedDistrict);

  return (
    <Layout>
      <div className="container py-8 space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold">Crime Heatmap</h1>
            <p className="text-muted-foreground mt-1">
              Geographic visualization of case density across districts
            </p>
          </div>
          <div className="flex items-center gap-3">
            <Select value={timeFilter} onValueChange={setTimeFilter}>
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="Time Period" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Time</SelectItem>
                <SelectItem value="month">This Month</SelectItem>
                <SelectItem value="quarter">This Quarter</SelectItem>
                <SelectItem value="year">This Year</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Legend */}
        <div className="flex flex-wrap items-center gap-6">
          <span className="text-sm font-medium">Intensity:</span>
          <div className="flex items-center gap-2">
            <div className="h-4 w-4 rounded bg-success" />
            <span className="text-sm">Low</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="h-4 w-4 rounded bg-warning" />
            <span className="text-sm">Medium</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="h-4 w-4 rounded bg-destructive" />
            <span className="text-sm">High</span>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Map Visualization */}
          <Card className="lg:col-span-2">
            <CardContent className="p-0">
              <div className="relative bg-muted/30 h-[500px] overflow-hidden rounded-lg">
                {/* Placeholder Map */}
                <svg width="100%" height="100%" viewBox="0 0 600 500">
                  {/* Delhi outline placeholder */}
                  <path
                    d="M100,100 L500,100 L500,400 L100,400 Z"
                    fill="hsl(var(--muted))"
                    stroke="hsl(var(--border))"
                    strokeWidth="2"
                  />
                  
                  {/* Grid lines */}
                  {[150, 200, 250, 300, 350].map((y) => (
                    <line
                      key={`h-${y}`}
                      x1="100"
                      y1={y}
                      x2="500"
                      y2={y}
                      stroke="hsl(var(--border))"
                      strokeWidth="0.5"
                      strokeDasharray="4"
                    />
                  ))}
                  {[150, 200, 250, 300, 350, 400, 450].map((x) => (
                    <line
                      key={`v-${x}`}
                      x1={x}
                      y1="100"
                      x2={x}
                      y2="400"
                      stroke="hsl(var(--border))"
                      strokeWidth="0.5"
                      strokeDasharray="4"
                    />
                  ))}

                  {/* Heatmap circles */}
                  {districtCounts.map((cell, index) => {
                    const x = 150 + (index % 4) * 100;
                    const y = 150 + Math.floor(index / 4) * 100;
                    const isSelected = selectedDistrict === cell.district;
                    return (
                      <g
                        key={cell.district}
                        onClick={() => setSelectedDistrict(cell.district)}
                        className="cursor-pointer"
                      >
                        <circle
                          cx={x}
                          cy={y}
                          r={20 + cell.count * 10}
                          className={getHeatColor(cell.count)}
                          opacity={isSelected ? 0.9 : 0.6}
                          stroke={isSelected ? 'hsl(var(--foreground))' : 'none'}
                          strokeWidth={isSelected ? 3 : 0}
                        />
                        <text
                          x={x}
                          y={y + 50}
                          textAnchor="middle"
                          className="fill-foreground"
                          style={{ fontSize: '10px' }}
                        >
                          {cell.district.split(' ')[0]}
                        </text>
                        <text
                          x={x}
                          y={y + 5}
                          textAnchor="middle"
                          className="fill-white font-bold"
                          style={{ fontSize: '14px' }}
                        >
                          {cell.count}
                        </text>
                      </g>
                    );
                  })}
                </svg>

                <div className="absolute bottom-4 left-4 bg-card/90 backdrop-blur-sm rounded-lg p-3 border border-border">
                  <p className="text-xs text-muted-foreground">Click on regions to see details</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* District Details Panel */}
          <div className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <Map className="h-5 w-5" />
                  District Details
                </CardTitle>
              </CardHeader>
              <CardContent>
                {selectedDistrictData ? (
                  <div className="space-y-4">
                    <div>
                      <p className="text-sm text-muted-foreground">Selected District</p>
                      <p className="font-semibold text-lg">{selectedDistrictData.district}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Total Cases</p>
                      <p className="text-3xl font-bold text-primary">
                        {selectedDistrictData.count}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Intensity Level</p>
                      <Badge
                        variant="outline"
                        className={
                          selectedDistrictData.count / maxCount > 0.7
                            ? 'bg-destructive/10 text-destructive border-destructive/20'
                            : selectedDistrictData.count / maxCount > 0.4
                            ? 'bg-warning/10 text-warning border-warning/20'
                            : 'bg-success/10 text-success border-success/20'
                        }
                      >
                        {selectedDistrictData.count / maxCount > 0.7
                          ? 'High'
                          : selectedDistrictData.count / maxCount > 0.4
                          ? 'Medium'
                          : 'Low'}
                      </Badge>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Coordinates</p>
                      <p className="font-mono text-sm">
                        {selectedDistrictData.lat.toFixed(4)}, {selectedDistrictData.lng.toFixed(4)}
                      </p>
                    </div>
                  </div>
                ) : (
                  <p className="text-sm text-muted-foreground">
                    Select a district from the map to view details
                  </p>
                )}
              </CardContent>
            </Card>

            {/* Top Districts */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <TrendingUp className="h-5 w-5" />
                  Top Districts
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {districtCounts
                    .sort((a, b) => b.count - a.count)
                    .slice(0, 5)
                    .map((district, index) => (
                      <div
                        key={district.district}
                        className="flex items-center justify-between cursor-pointer hover:bg-muted/50 p-2 rounded-lg transition-colors"
                        onClick={() => setSelectedDistrict(district.district)}
                      >
                        <div className="flex items-center gap-3">
                          <span className="text-sm font-medium text-muted-foreground w-5">
                            #{index + 1}
                          </span>
                          <span className="text-sm">{district.district}</span>
                        </div>
                        <Badge variant="secondary">{district.count}</Badge>
                      </div>
                    ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-primary/10 rounded-lg">
                  <Map className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <p className="text-2xl font-bold">{districtCounts.length}</p>
                  <p className="text-sm text-muted-foreground">Active Districts</p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-destructive/10 rounded-lg">
                  <AlertTriangle className="h-5 w-5 text-destructive" />
                </div>
                <div>
                  <p className="text-2xl font-bold">
                    {districtCounts.filter((d) => d.count / maxCount > 0.7).length}
                  </p>
                  <p className="text-sm text-muted-foreground">High Intensity</p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-warning/10 rounded-lg">
                  <Filter className="h-5 w-5 text-warning" />
                </div>
                <div>
                  <p className="text-2xl font-bold">{mockCases.length}</p>
                  <p className="text-sm text-muted-foreground">Total Cases</p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-success/10 rounded-lg">
                  <TrendingUp className="h-5 w-5 text-success" />
                </div>
                <div>
                  <p className="text-2xl font-bold">
                    {(mockCases.length / districtCounts.length).toFixed(1)}
                  </p>
                  <p className="text-sm text-muted-foreground">Avg per District</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </Layout>
  );
};

export default Heatmap;