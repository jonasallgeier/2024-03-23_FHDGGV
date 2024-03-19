clearvars

rng(sum('asdfasdafsdfa'))

pltWdth = 0.45*32.1;
pltHght = 0.45*45.95;
fig = figure(1);
fig.Units       = "centimeters";
  fig.PaperUnits  = "centimeters";
  fig.PaperSize   = [pltWdth,pltHght];
  fig.Position    = [0,0,pltWdth,pltHght];

clf(fig)

a = makedist('Lognormal','mu',log(2.5),'sigma',log(1.6));

% data = 3.5+3*rand(1e4,1);
data = 3.5+1*rand(5e3,1);
data = [data; 6.5-1*rand(5e3,1)];

data = [data; 4.5+1*rand(4e3,1)];
data = [data; 1+8*rand(7e3,1)];
% data = [data; 3+0.5*randn(3e3,1)];
% data = [data; 4+0.5*randn(3e3,1)];
b = fitdist(data(:),'Kernel','Kernel','normal','support',[0.95 9.05],'width',0.2);

xA = linspace(0,10,150);

t = tiledlayout(5,2,'TileIndexing','columnmajor');

nexttile(1)
plot(xA,a.pdf(xA),'LineWidth',2)
ylim([0 0.4])
xlim([0 10])
% yline(a.pdf(2.5))
xline(2.5)

nexttile(2)
plot(xA,b.pdf(xA),'LineWidth',2)
ylim([0 0.4])
xlim([0 10])
% yline(b.pdf(6.2))
xline(6.2)

nexttile(3)
axis off

nexttile(4)
plot(xA,a.cdf(xA),'LineWidth',2)
xline(2.5)
yline(a.cdf(2.5))

nexttile(5)
plot(xA,b.cdf(xA)+(xA>9),'LineWidth',2)
xline(6.2)
yline(b.cdf(6.2))

nexttile(9)
yL = linspace(0,1,150);
xL = log(yL./(1-yL));
x1 = log(a.cdf(2.5)./(1-a.cdf(2.5)));
plot(xL,yL,'LineWidth',2)
yline(a.cdf(2.5))
xline(x1)

nexttile(10)
x2 = log(b.cdf(6.2)./(1-b.cdf(6.2)));
plot(xL,yL,'LineWidth',2)
yline(b.cdf(6.2))
xline(x2)

nexttile(6)
plot(xL,exp(-xL)./(1+exp(-xL)).^2,'LineWidth',2)
xline(x1)
nexttile(7)
plot(xL,exp(-xL)./(1+exp(-xL)).^2,'LineWidth',2)
xline(x2)

t.TileSpacing = 'tight';
t.Padding = 'compact';


figure(2)

plot(xA,xL)
saveas(fig,'parSpace.png')


